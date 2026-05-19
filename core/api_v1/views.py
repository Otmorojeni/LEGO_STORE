from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Theme, Brand, Kit, Review
from .serializers import ThemeSerializer, BrandSerializer, KitSerializer, ReviewSerializer

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import CommentPermission

from drf_spectacular.utils import extend_schema


@extend_schema(request=ThemeSerializer, responses=ThemeSerializer)
@api_view(['GET', 'POST'])
def theme_list(request):
    if request.method == 'GET':
        themes = Theme.objects.all()
        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        is_many = isinstance(request.data, list)
        serializer = ThemeSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=ThemeSerializer, responses=ThemeSerializer)
@api_view(['GET', 'DELETE', 'PATCH'])
def theme_detail(request, pk):
    try:
        theme = Theme.objects.get(pk=pk)
    except Theme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ThemeSerializer(theme)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = ThemeSerializer(theme, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class KitListCreateView(ListCreateAPIView):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['theme', 'release_year']

    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = KitSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KitDetailView(GenericAPIView):
    serializer_class = KitSerializer
    
    def get(self, request, pk):
        try:
            kit = Kit.objects.get(pk=pk)
            serializer = KitSerializer(kit)
            return Response(serializer.data)
        except Kit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk):
        try:
            kit = Kit.objects.get(pk=pk)
            serializer = KitSerializer(kit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Kit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            kit = Kit.objects.get(pk=pk)
            kit.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Kit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class BrandListCreateView(GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, name=None):
        if name:
            brand = Brand.objects.filter(name=name)
        else:
            brand = Brand.objects.all()
        serializer = BrandSerializer(brand, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = BrandSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrandDetailView(GenericAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = BrandSerializer(brand)
            return Response(serializer.data)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
            serializer = BrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Brand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

class ReviewList(GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get(self, request, kit_id=None):
        if kit_id:
            reviews = Review.objects.filter(kit_id=kit_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = ReviewSerializer(data=request.data, many=is_many)
        user = self.request.user if self.request.user.is_authenticated else None
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewDetail(GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CommentPermission]

    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)