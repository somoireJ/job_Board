from rest_framework import serializers
from .models import JobListing, JobApplication, UserProfile, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    is_applicant = serializers.SerializerMethodField()
    is_employer = serializers.SerializerMethodField()

    def get_is_applicant(self, obj):
        return obj.applicant is not None

    def get_is_employer(self, obj):
        return obj.employer is not None

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'is_applicant', 'is_employer']



class ApplicantSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        user.set_password(password)
        user.is_applicant = True
        user.save()
        Applicant.objects.create(user=user)
        return user


class EmployerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        user.set_password(password)
        user.is_employer = True
        user.save()
        Employer.objects.create(user=user)
        return user
