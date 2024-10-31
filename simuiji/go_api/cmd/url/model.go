package url

import "time"

type Url struct {
	ShortUrl string    `json:"shortUrl"`
	LongUrl  string    `json:"longUrl"`
	IsEnable int       `json:"isEnable"`
	RegDate  time.Time `json:"regDate"`
	UrlId    int       `json:"urlId" gorm:"primaryKey"`
}

func (Url) TableName() string {
	return "url"
}
