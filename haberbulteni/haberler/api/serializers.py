from rest_framework import serializers
from haberler.models import Makale ,Gazeteci
from datetime import datetime,date
from django.utils.timesince import timesince



class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    class Meta:
        model = Makale
        fields = "__all__"
        # fields = ["yazar","baslık","metin"]
        # exclude = ["yazar","baslık","metin"]
        read_only_fields = ["id","yayinlanma_tarihi","güncellenme_tarihi"]
    def get_time_since_pub(self,object):
        now = datetime.now()
        pub_date = object.yayinlanma_tarihi
        time_delta = timesince(pub_date,now)
        return time_delta

    def validate_yayinlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError("Yayınlanma tarihi ileri bir tarih olmaz")
        return tarihdegeri


class GazeteciSerializer(serializers.ModelSerializer):
    # makaleler = MakaleSerializer(many=True,read_only=True)#read_only yeni bir yazar oluşturulunca
    makaleler = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="makale-detay"
    )

    class Meta:
        model = Gazeteci
        fields = "__all__"










class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayinlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    olusturulma_tarihi = serializers.DateTimeField(read_only=True)
    guncellenme_tarihi = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        print(validated_data)
        #validated_data arka planda dict geldiği için ** koymamız lazım key value için 
        return Makale.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # update var mı diye bakıyoruz
        instance.yazar = validated_data.get('yazar',instance.yazar)
        instance.baslik = validated_data.get('baslik',instance.baslik)
        instance.aciklama = validated_data.get('aciklama',instance.aciklama)
        instance.metin = validated_data.get('metin',instance.metin)
        instance.sehir = validated_data.get('sehir',instance.sehir)
        instance.yayinlanma_tarihi = validated_data.get('yayinlanma_tarihi',instance.yayinlanma_tarihi)
        instance.aktif = validated_data.get('aktif',instance.aktif)

        instance.save()
        return  instance

    def validate(self,data):
        if data["baslik"] == data["aciklama"]:
            raise serializers.ValidationError("Baslik ve açıklama aynı olamaz")
        return data 

    def validate_baslik(self,value):
        if len(value)<20:
            raise serializers.ValidationError("Baslik alanı min 20 karakter olmalı")
        return value


