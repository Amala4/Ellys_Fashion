from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Colour(models.Model):
    name = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ProductList(models.Model):
    status_choices = (
       ('In Stock', 'In Stock'),
       ('Out of stock', 'Out of stock')
    )

    size_choices = (
       ('N/A', 'N/A'),
       ('XSmall', 'XSmall'),
       ('Small', 'Small'),
       ('Medium', 'Medium'),
       ('Large', 'Large'),
       ('XLarge', 'XLarge')
    )

    gender_choices = (
       ('male', 'male'),
       ('female', 'female'),
       ('kids', 'kids'),
       ('both', 'both')
    )

    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200,  null=True, blank=True, help_text= "(Optional) If the brand is unknown you can leave this field blank")
    price = models.IntegerField()
    promo_price = models.IntegerField( null=True, blank=True, help_text= "(Optional) Fill this only if you have a promo price for this item")
    post_date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="products")
    colour = models.ManyToManyField(Colour)
    gender = models.CharField(max_length=50, choices=gender_choices, default='female')
    description = models.TextField(blank=True)
    is_published = models.BooleanField("Publish Post", help_text= "Uncheck this button if you want this post to stop showing on the website", default=True)
    best_seller = models.BooleanField(default=False, help_text= "(Optional) Check this button if this item is among your best selling items")
    hot_trend = models.BooleanField(default=False, help_text= "(Optional) Check this button if this item is a hot trend")
    feature = models.BooleanField(default=False, help_text= "(Optional) Check this button if you want this item to stay top on the website")
    availability = models.CharField(max_length=50, choices=status_choices, default='In Stock')
    size = models.CharField(max_length=50, choices=size_choices, default='Medium')
    photo_1 = models.ImageField(upload_to= 'media/products/')
    photo_2 = models.ImageField(upload_to= 'media/products/', blank=True)
    photo_3 = models.ImageField(upload_to= 'media/products/', blank=True)
    photo_4 = models.ImageField(upload_to= 'media/products/', blank=True)



    class Meta:
        verbose_name_plural = "Product List"

    def __str__(self):
        return self.name



    
    




