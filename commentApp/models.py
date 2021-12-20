from django.db import models


class CommentLocation(models.Model):
    comment = models.TextField()
    user = models.ForeignKey("userApp.User", on_delete=models.CASCADE,
                             verbose_name="Пользователь оставивший коментарий")
    location = models.ForeignKey(
        "locationApp.Location", on_delete=models.CASCADE, related_name="comments")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.user.fullname, self.comment[:10])


class ReviewLocation(models.Model):
    review = models.IntegerField()
    user = models.ForeignKey("userApp.User", on_delete=models.CASCADE,
                             verbose_name="Пользователь оставивший оценку")
    location = models.ForeignKey(
        "locationApp.Location", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return "{} {}".format(self.user.fullname, self.review)


class   CommentSpecialist(models.Model):
    comment = models.TextField()
    user = models.ForeignKey("userApp.User", on_delete=models.CASCADE,
                             verbose_name="Пользователь оставивший коментарий")
    specialist = models.ForeignKey("specialistApp.Specialist",
                                   related_name="comments",
                                   on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.user.fullname, self.comment[:10])


class ReviewSpecialist(models.Model):
    review = models.IntegerField()
    user = models.ForeignKey("userApp.User", on_delete=models.CASCADE,
                             verbose_name="Пользователь оставивший оценку")
    specialist = models.ForeignKey(
        "specialistApp.Specialist", related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.fullname, self.review)
