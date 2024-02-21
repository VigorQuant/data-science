# Hierarchical clustering

## read data from csv
J2013 <- read.csv("C:/.../datasets/J2013.CSV",check.names = FALSE)
## Print the first two rows of this processed data.
J2013[1:2,]

## change substation column as character
J2013$Substation <- as.character(J2013$Substation)
## group J2013 by Substation, and calculate mean of each column
J2013_groupby <- group_by(J2013,Substation) %>% dplyr::summarise(across(.fns = mean))
## delete useless column Data
J2013_groupby$Date <- NULL
## Print the first two rows of this processed data.
J2013_groupby[1:2,]

## 2.3
## standardize the dataframe J2013_groupby
df <- scale(J2013_groupby[2:145])
## calculate the euclidean distance
d <- dist(df,method='euclidean')
## using "complete" to clustering 
hc <- hclust(d,method='complete')
## show the clustered tree
plot(hc,hang=-1)
## Showing the effect of cutting trees at different heights
rect.hclust(hc, h = 25, border = 3:4)
rect.hclust(hc, h = 22, border = 3:4)

## cut tree for 5 categories 
groups.5 <- cutree(hc,7)
## add groups column for 5 categories
J2013_groupby$groups <- groups.5
## show the number of substations in each of my clusters
table(groups.5)

## make a new df for pca
df_pca <- J2013_groupby[,2:145]
## calculate the PCA result
pca <- prcomp(df_pca,scale = T)
## process data
df_pca_x <- data.frame(pca$x)
df_pca_x$groups <- J2013_groupby$groups
df_pca_x$groups <- as.factor(df_pca_x$groups)
## show the picture of distribution after PCA
ggplot(df_pca_x,aes(x = PC1,y = PC2,shape=groups,color=groups))+
  geom_point()+
  scale_shape_manual(values = c(1,2,3,4,5,6,7))+
  labs(title = "Post-clustering PCA downscaled projection map")

## functions data disposal
data_disposal <- function(df,groups.x){
  df$groups <- as.factor(df$groups)
  ## delete useless column
  df <- df[,-1]
  ## group dataframe J2013_weekends_groupby by groups, and calculate mean for each columns
  df_factor <- group_by(df,groups) %>%
    dplyr::summarise_each(funs(mean))
  
  ## Matrix transpose for ploting
  df_factor_t <- t(df_factor)
  ## change the colnames
  colnames(df_factor_t) <- df_factor_t[1,]
  ## delete the first columns
  df_factor_t <- df_factor_t[-1,]
  ## save as data.frame
  df_t <- data.frame(df_factor_t)
  
  ## add time column
  df_t$time <- colnames(df_factor[,2:145])
  
  for(i in 1:max(groups.x)){
    df_t[,i] <- as.numeric(df_t[,i])
  }
  
  values <- c()
  category <- c()
  time <- c()
  n <- ncol(df_t)-1
  for (i in 1:n){
    values <- c(values,as.vector(unlist(df_t[,i])))
    category <- c(category,rep(colnames(df_t[i]),times = 144))
    time <- c(time,df_t$time)
  }
  df_t <- data.frame(values,category,time)
  df_t$time <- as.POSIXct(strptime(df_t$time,"%H:%M"))
  return(df_t)
}

## using data_disposal function to deal with this dataframe
J2013_t <- data_disposal(J2013_groupby,groups.5)
##write_excel_csv(x = J2013_t,file = "C:/Users/l4241/OneDrive/Exeter/HM503/Assignment/datasets/J2013_t.CSV")

## plot 5 categories point figures
ggplot(aes(x=time,y = values),data = J2013_t)+
  geom_point()+
  scale_x_datetime(date_labels=("%H:%M"))+
  ylab("Electricity usage")+
  labs(title="Average daily demand curves for the seven clusters")+
  facet_wrap(~category)

## read CSV
J2013_weekends <- read.csv("C:/Users/l4241/OneDrive/Exeter/HM503/Assignment/datasets/J2013_weekends.CSV",check.names = FALSE)

## group J2013_weekends by sub_week, and calculate mean for each columns
J2013_weekends_groupby <- group_by(J2013_weekends,sub_week) %>%
  dplyr::summarise_each(funs(mean))
## vlookup groups from J2013_groupby to groups.week by "Substation"
groups.week <- c()
for(i in 1:nrow(J2013_weekends_groupby)){
  groups.week <- c(groups.week,J2013_groupby$groups[J2013_groupby$Substation == J2013_weekends_groupby$Substation[i]])  
}

J2013_weekends_groupby$groups <- groups.week
J2013_weekends_groupby$weekends <- apply(J2013_weekends_groupby[,1], 2, function(x) substring(x, 8, nchar(x)))
J2013_weekends_groupby$weekends <- as.vector(unlist(J2013_weekends_groupby$weekends))
colnames(J2013_weekends_groupby[,148]) <- "weekends"

## using data_disposal function deal with this dataframe
## functions data disposal
J2013_weekends_groupby$groups <- as.factor(J2013_weekends_groupby$groups)
J2013_weekends_groupby$weekends <- as.factor(J2013_weekends_groupby$weekends)
## delete useless column
J2013_weekends_groupby <- J2013_weekends_groupby[,-1]


## group dataframe J2013_weekends_groupby by groups, and calculate mean for each columns
df_grouped <- J2013_weekends_groupby %>% group_by(groups,weekends)
df_factor <- df_grouped %>% summarise_each(funs(mean))

## Matrix transpose for ploting
df_factor_t <- t(df_factor)
## change the colnames
colnames(df_factor_t) <- df_factor_t[1,]
## delete the first columns
df_factor_t <- df_factor_t[-3,]
## save as data.frame
df_t <- data.frame(df_factor_t)

values <- c()
category <- c()
time <- c()
weekend <- c()
n <- ncol(df_t)
for (i in 1:n){
  values <- c(values,as.vector(unlist(df_t[3:146,i])))
  category <- c(category,rep(df_t[1,i],times = 144))
  weekend <- c(weekend,rep(df_t[2,i],times = 144))
  time <- c(time,colnames(J2013_weekends_groupby[,2:145]))
}
J2013_weekends_plot <- data.frame(values,category,weekend,time)
J2013_weekends_plot$time <- as.POSIXct(strptime(J2013_weekends_plot$time,"%H:%M"))
J2013_weekends_plot$values <- as.numeric(J2013_weekends_plot$values)

## plot the distribution figure
ggplot(aes(x=time,y = values),data = J2013_weekends_plot)+
  geom_point(aes(color = weekend))+
  scale_x_datetime(date_labels=("%H:%M"))+
  labs(title="Compare the average daily demand curves of the seven clusters on weekends and weekdays",size=4)+
  facet_wrap(~category)

## processing data
## loading data
Characteristics <- read.csv("C:/Users/l4241/OneDrive/Exeter/HM503/Assignment/datasets/Characteristics.csv")
substation_list <- J2013_groupby$Substation
df_chara <- Characteristics[Characteristics$SUBSTATION_NUMBER %in% substation_list,]
## Data de-duplication
df_chara <- df_chara[!duplicated(df_chara),]
df1 <- data.frame(substation_list,groups.5)
df1 <- df1[order(df1$substation_list),]
df2 <- df_chara[order(df_chara$SUBSTATION_NUMBER),]
df2$groups <- df1$groups.5
## Data segmentation
substation_analysis1 <- df2[,c(2,8)]
substation_analysis2 <- df2[,c(3,4,5,6,8)]
substation_analysis1$groups <- as.factor(substation_analysis1$groups)

## plot the figure P1
ggplot(data=substation_analysis1,aes(groups,fill=TRANSFORMER_TYPE))+
  geom_bar(stat='count',position = 'stack')+
  geom_text(aes(y=..count..,label=..count..),stat='count',position = 'stack',size=3)+
  labs(title="The number of each TYPE in each groups")

## peocessing data
substation_analysis1_groupby <- substation_analysis1 %>%
  group_by(groups,TRANSFORMER_TYPE) %>%
  dplyr::summarise(count=n())
substation_analysis1_groupby$percentages <- substation_analysis1_groupby$count / sum(substation_analysis1_groupby$count)
substation_analysis1_groupby2 <- ddply(substation_analysis1_groupby,'groups',transform,percentage_type = count/sum(count)*100)
## plot the figure P2
ggplot(data=substation_analysis1_groupby2,aes(x = groups, y = percentage_type, fill=TRANSFORMER_TYPE))+
  geom_bar(stat='identity',position = 'stack')+
  scale_y_continuous(breaks=seq(0,100,25),
                     labels=c('0','25%','50%','75%','100%'))+
  geom_text(aes(label = paste0(round(percentage_type,1),"%")),position = 'stack',size = 3)+
  labs(title = "The percentage of each TYPE in each groups")

substation_analysis2_groupby <- group_by(substation_analysis2,groups) %>% 
  dplyr::summarise(across(.fns = mean))
substation_analysis2_groupby