from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parents', 'children', 'siblings']

    def validate(self, data):
        validation_data = self._kwargs['data']
        if validation_data.get('children'):
            vd = validation_data['children']
            for obj in vd:
                if CategoriesSerializer(data=obj).is_valid():
                    return data
                raise serializers.ValidationError('validation error in nested object')
        return data

    def get_parents(self, obj):
        r = self.context['request']
        if r.method == 'GET':
            if obj.parent_id is None:
                return []
            parent_obj = Category.objects.get(id=obj.parent_id)
            return [CategorySerializer(parent_obj).data] + self.get_parents(parent_obj)

    def get_children(self, obj):
        r = self.context['request']
        if r.method == 'GET':
            objects = Category.objects.filter(parent_id=obj.id)
            return [CategorySerializer(obj).data for obj in objects]

    def get_siblings(self, obj):
        r = self.context['request']
        if r.method == 'GET':
            objects = Category.objects.filter(parent_id=obj.parent_id).exclude(id=obj.id)
            return [CategorySerializer(obj).data for obj in objects]

    def create(self, validated_data):
        parent = None
        if self.context.get('parent'):
            parent = self.context.get('parent')
        inst = Category.objects.create(name=validated_data['name'], parent_id=parent)
        if self._kwargs['data'].get('children'):
            r_context = self._kwargs['data']['children']
            for obj in r_context:
                self.context['parent'] = inst.id
                vd = CategoriesSerializer(data=obj, context=self.context)
                if vd.is_valid():
                    vd.save()
            return inst
        else:
            return inst
