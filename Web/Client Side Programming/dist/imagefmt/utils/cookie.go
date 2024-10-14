package utils

import (
	"net/http"
	"time"
)

func SetCookie(token string, w http.ResponseWriter) {
	expiration := time.Now().Add(CookieDuration)
	cookie := http.Cookie{
		Name:     CookieName,
		Value:    token,
		Expires:  expiration,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
		SameSite: http.SameSiteNoneMode,
	}
	http.SetCookie(w, &cookie)
}

func SetToken(claims map[string]interface{}, w http.ResponseWriter) error {
	auth := NewJWT(SecretKey)
	token, err := auth.GenerateToken(claims)
	if err != nil {
		return err
	}
	SetCookie(token, w)
	return nil
}
