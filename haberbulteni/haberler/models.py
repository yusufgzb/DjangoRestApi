from django.db import models

# Create your models here.
class Gazeteci(models.Model):
    isim = models.CharField(max_length=120)
    soyisim = models.CharField(max_length=120)
    biyografi = models.TextField()
    
    def __str__(self):
        return f'{self.isim} {self.soyisim}'

class Makale(models.Model):
    yazar = models.ForeignKey(Gazeteci,on_delete=models.CASCADE,default="anonim")
    yazar = models.CharField(max_length=150)
    baslik = models.CharField(max_length=120)
    aciklama = models.CharField(max_length=200)
    metin = models.TextField()
    sehir = models.CharField(max_length=120)
    yayinlanma_tarihi = models.DateField()
    aktif = models.BooleanField(default=True)
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.baslik