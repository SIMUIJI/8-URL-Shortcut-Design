package model

import "time"

type Url struct {
	ShortUrl string    `json:"short_url"`
	LongUrl  string    `json:"long_url"`
	IsEnable int       `json:"is_enable"`
	RegDate  time.Time `json:"reg_date"`
	UrlId    int       `json:"url_id" gorm:"primaryKey"`
}

func (Url) TableName() string {
	return "url"
}
