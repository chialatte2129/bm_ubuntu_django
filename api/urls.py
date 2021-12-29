#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url, include
from api.redirect import service
from api.sale_record import service as sale_record_service

urlpatterns = [
    ###account
    url('redirect/get_url', service.GetUrlPath.as_view()),
    url('sale_info/record', sale_record_service.SaleInfoRecord.as_view()),

]

