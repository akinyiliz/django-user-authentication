
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import *
from rest_framework_simplejwt.tokens import AccessToken


@api_view(['POST'])
def CreateUser(request):
    if request.method == 'POST':
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                access_token = AccessToken.for_user(user)
                res = {
                    "status": "success",
                    "message": "Registration Successful",
                    "data": {
                        'accessToken': str(access_token),
                        "user": serializer.data
                    }
                }
                return Response(res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {
                    "status": "Bad request",
                    "message": "Registration unsuccessful",
                    "statusCode": 400
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = []
            for field, error_list in serializer.errors.items():
                for error in error_list:
                    errors.append({"field": field, "message": str(error)})
            return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
def UserLogin(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            res = {
                "status": "success",
                "message": "Login Successful",
                "data": serializer.validated_data
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            errors = []
            for field, error_list in serializer.errors.items():
                for error in error_list:
                    errors.append({"field": field, "message": str(error)})
            return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
def GetUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Userserializer(user)
    res = {
        "status": "success",
        "message": "Retrieval Successful",
        "data": serializer.data
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensures user must be authenticated
def Getorganizations(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    organizations = request.user.organizations.all()
    serializer = OrganizationSerializer(organizations, many=True)
    res = {
        "status": "success",
        "message": "Query Successful",
        "data": {
            "organisations": serializer.data
        }
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOrganization(request, org_id):
    try:
        organization = request.user.organizations.get(orgId=org_id)
    except Organization.DoesNotExist:
        return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
    except AttributeError:
        return Response({"error": "User does not have attribute 'organizations'"}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrganizationSerializer(organization)
    res = {
        "status": "success",
        "message": "Query Successful",
        "data": serializer.data
    }
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateOrganization(request):
    serializer = OrganizationSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        try:
            organization = serializer.save()
            res = {
                "status": "success",
                "message": "Organization created successfully",
                "data": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = {
                "status": "Bad Request",
                "message": "Client error",
                "statusCode": 400
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
    else:
        errors = []
        for field, error_list in serializer.errors.items():
            for error in error_list:
                errors.append({"field": field, "message": str(error)})
        return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
def AddUserToOrganization(request, org_id):
    serializer = AddorganizationSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['userId']
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            res = {
                "status": "User Not found",
                "message": "Client error",
                "statusCode": 404
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        try:
            # organization = request.user.organizations.get(pk=pk)
            organization = request.user.organizations.get(orgId=org_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        user.organizations.add(organization)
        user.save()
        res = {
            "status": "success",
            "message": "User added to organization successfully",
        }
        return Response(res, status=status.HTTP_200_OK)
    else:
        errors = []
        for field, error_list in serializer.errors.items():
            for error in error_list:
                errors.append({"field": field, "message": str(error)})
        return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
