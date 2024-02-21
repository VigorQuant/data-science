# Initial data analysis

## load Data
load("C:/.../datasets/January_2013.RData")
df <- read.csv("C:/.../datasets/Characteristics.csv")

## the distributions of Percentage_IC
ggplot(data=df)+
  geom_density(aes(x=Percentage_IC))+
  labs(title = "Density of Percentage_IC")

## plot the distributions of Transformer_RATING
p2 <- ggplot(data=df,aes(x=Transformer_RATING,y =..count..))+
  geom_histogram(aes(x=Transformer_RATING),binwidth = 100)+
  geom_text(aes(y=..count..,label=..count..),stat='bin',binwidth = 100,vjust = -0.5)+
  ylab("The number of Substation")+
  labs(title = "Distribution of Transformer_RATING")


## the distributions of Transformer_RATING
## disposal data
df$TRANSFORMER_TYPE <- as.factor(df$TRANSFORMER_TYPE)
df1 <- group_by(df,TRANSFORMER_TYPE) %>%
  dplyr::summarise(count=n())
df1$type <- c("Type","Type")

## plot the figure
ggplot(data=df1,aes(x=type,y=count,fill=TRANSFORMER_TYPE))+
  geom_bar(stat='identity',position = 'stack')+
  coord_polar("y",start=0)+
  geom_text(aes(label=count),position = position_stack(vjust = 0.5))+
  xlab("")+
  ylab("Number of each Tpye")+
  labs(title = "Share of each TRANSFORMER_TYPE")

## describe the relationships between those factors
ggpairs(df[,2:6])+
  theme(strip.text.x = element_text(size = 6),
        strip.text.y = element_text(size = 4))+
  labs(title = "Matrix Scatter Plot of each variables")




