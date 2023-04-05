from django.db import models


class Log(models.Model):
    LOG_LEVELS = {
        ("DBG", "Debug"),
        ("INF", "Info"),
        ("WRN", "Warning"),
        ("ERR", "Error")
    }
    dt = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    level = models.CharField(max_length=3, choices=LOG_LEVELS, null=False, blank=False)

    def __str__(self):
        return f"[{self.dt}] {dict(self.LOG_LEVELS)[self.level]}: {self.message}"


class Notify(models.Model):
    ts = models.DateTimeField(blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.ts.strftime('%Y-%m-%d %T+%Z')}: {self.message}"
