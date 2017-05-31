# File that reads .csv file of combined date interval topic analysis results from ConText Application.
# Plots the topics in a bar graph
library(ggplot2)
library(grid)


#read in 7 Topic Analysis file for Amazon Echo and Google Home
combined_topic<-read.csv("../../data/topic/Topic_Analysis/data-RS-W-TopicModeling.csv")
combined_topic$device<-c("Amazon Echo", "Google Home")

# Giving the topics a name
# Music Topic 1: phone - update - room - echo - setup - app - music - working - devices - amazonecho - 
# Conversation Topic 2: alexa - echo - app - work - great - conversation - home - updated - call - wife -
# Sound Topic 3: iphone - works - answer - sounds - amazon - loud - information - register - dad - fun - 
# Apps Incident Topic 4: app - call - icon - set - work - galaxy - message - dot - android - device - 
# iOT Topic 5: amazonecho - iot - buy - control - make - apple - http://bit.ly - chromecast - great - ads - 
# Features Topic 6: amazon - feature - alexa - contacts - account - option - uninstalled - echos - app - code -
# Assistant Topic 7:googlehome - google - home - echo - amazon - play - alexa - love - music - assistant -

#Adding topics as column names
colnames(combined_topic)<- c("File Name","Music","Conversation", "Sound", "Apps", "iOT", "Features" ,"Assistant", "Device")

# Plotting frame
topic_list <- c("Music","Conversation", "Sound", "Apps", "iOT", "Features" ,"Assistant")
plotting_frame <- NULL
for(index_for_topic in seq(along=topic_list)) {
  this_topic_data_frame<-combined_topic[,c("Device", topic_list[index_for_topic])]
  colnames(this_topic_data_frame) <-c("Device","Weight")
  this_topic_data_frame$Topic <- rep(topic_list[index_for_topic],length=nrow(this_topic_data_frame))
  plotting_frame<-rbind(plotting_frame,this_topic_data_frame)
}

print(str(plotting_frame))

# use ggplot to plot graph
ggplot_object <- ggplot(plotting_frame,
                        aes(x=Device, y=Weight, fill=Topic)) +
  geom_bar(stat="identity") +
  scale_fill_manual(values = c("brown", "red", "lightgreen","blue","yellow", "black", "orange"))+
  ylab("Topic Weight")+
  xlab("")+
  ggtitle(paste("Amazon Echo vs Google Home Topic Analysis"))


print(ggplot_object)
ggsave("../../output/amazon_google_topic.pdf")

dev.off()
  