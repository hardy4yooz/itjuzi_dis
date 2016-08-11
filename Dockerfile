FROM python:3.5
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
COPY spiders.py /usr/local/lib/python3.5/site-packages/scrapy_redis
CMD /usr/local/bin/scrapy crawl itjuzi_dis
