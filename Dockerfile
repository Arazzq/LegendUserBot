# FROM kısmını Değiştirmeyiniz Epicye DockerFile Kullanın

FROM Arazzq/LegendUserBot:latest
RUN git clone https://github.com/erdewbey/OwenUserBot /root/Legend
WORKDIR /root/Legend
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
