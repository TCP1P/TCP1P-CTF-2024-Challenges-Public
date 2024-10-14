package utils

import "time"

const (
	SecretKey      = "secret"
	CookieName     = "authToken"
	CookieDuration = 30 * time.Minute
	UploadPath     = "./uploads/"
)
