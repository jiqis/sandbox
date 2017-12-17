#ƒtƒ@ƒCƒ‹
data <- read.csv("./data.csv")
data.temp<-data$average_temperature
data.dlen<-data$day_length
m1<-lm(data.temp~data.dlen)
summary(m1)