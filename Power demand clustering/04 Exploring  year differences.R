# Exploring differences between years

load("C:/.../datasets/January_2014.RData")
load("C:/.../datasets/January_2015.RData")

## combind two dataframe as one
J1415 <- rbind(January_2014,January_2015)
J1415$year <- substr(J1415$Date,1,4)
J1415$Date <- NULL

J1415$Substation <- as.character(J1415$Substation)
J1415$year <- as.character(J1415$year)

J1415_data <- J1415
J1415_data$Substation <- NULL
J1415_data$year <- NULL

J1415_data <- read.csv("C:/Users/l4241/OneDrive/Exeter/HM503/Assignment/datasets/J1415_data.CSV",check.names = FALSE)
J1415[,2:145] <- J1415_data
df <- J2013
df$year <- substr(df$Date,1,4)
df$Date <- NULL
J2013_year <- df
J131415 <- rbind(J2013_year,J1415)

## vlookup groups from J2013_groupby to groups.week by "Substation"
J131415_groups <- c()
for(i in 1:nrow(J131415)){
  J131415_groups <- c(J131415_groups,J2013_groupby$groups[J2013_groupby$Substation == J131415$Substation[i]])  
}
J131415$groups <- J131415_groups

## groupby data
df_grouped <- J131415 %>% group_by(groups,year)
J131415_groupby <- df_grouped %>%
  dplyr::summarise_each(funs(mean))
J131415_groupby$Substation <- NULL
J131415_groupby$groups <- as.character(J131415_groupby$groups)

## Restructuring of the data
values <- c()
category <- c()
time <- c()
year <- c()
n <- nrow(J131415_groupby)
for (i in 1:n){
  values <- c(values,as.vector(unlist(J131415_groupby[i,3:146])))
  category <- c(category,rep(as.character(J131415_groupby[i,1]),times = 144))
  year <- c(year,rep(as.character(J131415_groupby[i,2]),times = 144))
  time <- c(time,colnames(J2013_weekends_groupby[,2:145]))
}

## processing data
J345_plot <- data.frame(values,category,year,time)
J345_plot$category <- as.factor(J345_plot$category)
J345_plot$time <- as.POSIXct(strptime(J345_plot$time,"%H:%M"))

## plot the distribution figure
ggplot(aes(x=time,y = values),data = J345_plot)+
  geom_point(aes(color = year))+
  scale_x_datetime(date_labels=("%H:%M"))+
  facet_wrap(~category)+
  ylim(0,1)+
  labs(title="Comparing the three-year daily average curves of each cluster")+
  ylab("Electricity usage")


## 4.1
## processing data
df_grouped <- J1415 %>% group_by(Substation,year)
J1415_groupby <- df_grouped %>% summarise_each(funs(mean))

## Classification using KNN
df_year_knn <- knn(scale(J2013_groupby[,2:145]),scale(J1415_groupby[,3:146]),cl = as.vector(unlist(J2013_groupby[,146])),k=3)
values_knn <- as.vector(unlist(df_year_knn))
values_knn <- paste0("X",df_year_knn)
cate_list <- values_knn[!duplicated(df_year_knn)]

## processing data
Substationlist <- c(J2013_groupby$Substation,J1415_groupby$Substation)
yearlist <- c(rep("2013",times = length(J2013_groupby$Substation)),J1415_groupby$year)
groupslist <- c(J2013_groupby$groups,df_year_knn)
df <- data.frame(Substationlist,yearlist,groupslist)
df1 <- data.frame(Substationlist,groupslist)
df2 <- df1[!duplicated(df1),]

## calculate the list of substation which be classified to different clusters during 3 three
duplist <- group_by(df2,Substationlist) %>% dplyr::summarise(count=n())
## calculate the list of substation which be classified to 2 different clusters during 3 three
duplist2 <- duplist$Substationlist[duplist$count > 1]
## calculate the list of substation which be classified to 3 different clusters during 3 three
duplist3 <- duplist$Substationlist[duplist$count > 2]

## show the list
df4 <- df[order(df$Substationlist),]
df5 <- df4[df4$Substationlist %in% duplist2,]
colnames(df5)[3] <- "groups"
df5[1:10,]

# The first 10 rows of data results are shown here, and the grouping of these substations has changed.

nrow(df5) / 3
nrow(df5) / nrow(df)

df_grouped <- J131415 %>% group_by(Substation,year)
J131415_groupby_sub <- df_grouped %>% summarise_each(funs(mean))

J131415_groupby_sub$groups <- df1$groupslist
J345_51106 <- J131415_groupby_sub[J131415_groupby_sub$Substation == duplist3[1],]

values <- c()
time <- c()
year <- c()
n <- nrow(J345_51106)
for (i in 1:n){
  values <- c(values,as.vector(unlist(J345_51106[i,3:146])))
  year <- c(year,rep(as.character(J345_51106[i,2]),times = 144))
  time <- c(time,colnames(J2013_weekends_groupby[,2:145]))
}

J345_51106_plot <- data.frame(values,year,time,J131415_groupby_sub$groups[df1$Substationlist == duplist3[1]])
J345_51106_plot$time <- as.POSIXct(strptime(J345_51106_plot$time,"%H:%M"))

ggplot(aes(x=time,y = values),data = J345_51106_plot)+
  geom_point(aes(color = year))+
  scale_x_datetime(date_labels=("%H:%M"))+
  scale_color_manual(values = c("#00AFBB","#00A006","black"))+
  labs(title = paste0("Comparing the three-year daily average curves of Substation",duplist3[1]," of each cluster"))+
  ylab("Electricity usage")+
  ylim(0,1)

df6 <- df4[df4$Substationlist %in% duplist3,]
colnames(df6)[3] <- "groups"
df6


