# Allocating new substations to clusters

## reload data
load("C:/.../datasets/new_substations.RData")
## save this dataframe as new df 
NS <- new_substations

## select 3 to 146 columns
NS <- NS[,3:146]
## count the observations 
n = nrow(NS)
## for circulation
## each row will divide the max number of this row
for (i in 1:n){
  NS[i,] <- NS[i,] / max(NS[i,])
}

## add data and substation columnes to NS dataframe
NS <- data.frame(new_substations[,1:2],NS,check.names = FALSE)

## Omit comments with previously duplicated code
## calculate the weekends
NS$Date <- as.Date(NS$Date,format = "%Y-%m-%d")
Sys.setlocale("LC_TIME", "English")
NS$weekdays <- weekdays(NS$Date)
NS$weekends <- "workdays"
NS$weekends[NS$weekdays %in% c("Saturday","Sunday")] <- "weekend"

NS_W <- NS
NS_W$week <- NS_W$weekends
NS_W$Date <- NULL
NS_W$weekdays <- NULL
NS_W$weekends <- NULL


NS_w_groupby <- NS_W %>% group_by(Substation,week) %>%
  dplyr::summarise(across(.fns = mean))

## plot disposal data
substation <- c()
week <- c()
values <- c()
time <- c()
n <- nrow(NS_w_groupby)
for (i in 1:n){
  substation <- c(substation,rep(as.character(NS_w_groupby[i,1]),144))
  week <- c(week,rep(as.character(NS_w_groupby[i,2]),144))
  values <- c(values,as.vector(unlist(NS_w_groupby[i,3:146])))
  time <- c(time,colnames(J2013_groupby[i,2:145]))
}
NS_week_gb_df <- data.frame(substation,week,values,time)

NS_week_gb_df$week <- as.factor(NS_week_gb_df$week)
NS_week_gb_df$substation <- as.factor(NS_week_gb_df$substation)
NS_week_gb_df$time <- as.POSIXct(strptime(NS_week_gb_df$time,"%H:%M"))
ggplot(aes(x=time,y=values,color = week),data=NS_week_gb_df)+
  geom_point()+
  scale_x_datetime(date_labels=("%H:%M"))+
  facet_wrap(~substation)+
  labs(title="Comparing difference of weekdays and weekends for each substation")

NS$weekdays <- NULL
NS$weekends <- NULL
NS$Date <- NULL

NS_groupby <- group_by(NS,Substation) %>%
  dplyr::summarise_each(funs(mean))

test <- predict(pca,newdata = NS_groupby[,2:145])
df_pre <- data.frame(test[,1:2])
df_pca_x2 <- df_pca_x[,c(1,2,145)]
df_pre$groups <- c("S1","S2","S3","S4","S5")
df <- rbind(df_pca_x2,df_pre)
colorslist <- colors()[31:37]

ggplot(df,aes(x = PC1,y = PC2,color=groups,shape=groups))+
  geom_point()+
  scale_color_manual(values = c(colorslist,"black","black","black","black","black"))+
  scale_shape_manual(values = c(0,1,0,1,0,1,0,8,8,8,8,8))+
  labs("Clustering result two-dimensional projection map, add new substation")

groups7_groupby <- J2013_groupby[,2:146] %>% group_by(groups) %>%
  dplyr::summarise_each(funs(mean))
NS_gy <- NS_groupby
colnames(NS_gy)[1] <- "groups"
NS_plot <- rbind(NS_gy,groups7_groupby)
test2 <- predict(pca,newdata = NS_plot[,2:145])
df_pre2 <- data.frame(test2[,1:2])
df_pre2$groups <- as.factor(NS_plot$groups)
ggplot(df_pre2,aes(x = PC1,y = PC2,label = groups,color=groups))+
  geom_text()+
  scale_color_manual(values = c(colorslist,"black","black","black","black","black"))+
  labs(title = "New substation and clustering results_1")

ggplot(df,aes(x = PC1,y = PC2,label = groups,color=groups))+
  geom_text()+
  scale_color_manual(values = c(colorslist,"black","black","black","black","black"))+
  labs(title = "New substation and clustering results_2")


df_NS <- data.frame(NS_groupby[,1],c(3,2,1,2,1))
colnames(df_NS)[2] <- "groups"
df_NS

NS_chara <- Characteristics[Characteristics$SUBSTATION_NUMBER %in% df_NS$Substation,]
NS_chara

df_knn <- knn(J2013_groupby[,2:145],NS_groupby[,2:145],cl = as.vector(unlist(J2013_groupby[,146])),k=3)
df_knn

values_knn <- as.vector(unlist(df_knn))
values_knn <- paste0("X",values_knn)
cate_list <- values_knn[!duplicated(values_knn)]
prediction <- data.frame(rep("new",5),values_knn,NS_groupby[,2:145])

values <- c()
category <- c()
time <- c()
mark <- c()
n <- nrow(prediction)
for (i in 1:n){
  values <- c(values,as.vector(unlist(prediction[i,3:146])))
  mark <- c(mark,rep(prediction[i,1],times = 144))
  category <- c(category,rep(prediction[i,2],times = 144))
  time <- c(time,colnames(J2013_weekends_groupby[,2:145]))
}
new_subs <- data.frame(values,mark,category,time)
J2013_t$mark <- rep("standard",times = length(J2013_t$category))
new_subs <- data.frame(values,mark,category,time)
new_subs$time <- as.POSIXct(strptime(new_subs$time,"%H:%M"))
new_subs <- new_subs[,c("values","category","time","mark")]
compare_subs <- rbind(new_subs,J2013_t)

sub_plot <- compare_subs[compare_subs$category %in% cate_list,]

## plot the distribution figure
ggplot(aes(x=time,y = values),data = sub_plot)+
  geom_point(aes(color = mark))+
  scale_x_datetime(date_labels=("%H:%M"))+
  facet_wrap(~category)+
  labs(title="Comparing new substations and their classification results")+
  ylab("Electricity usage")+
  ylim(0,1)


       
      