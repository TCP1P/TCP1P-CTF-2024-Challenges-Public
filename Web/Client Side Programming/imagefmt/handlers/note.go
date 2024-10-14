package handlers

import (
	"imagefmt/utils"
	"net/http"

	"github.com/dgrijalva/jwt-go"
)

func SetNoteHandler(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims) {
	claims["note"] = r.FormValue("note")
	claims["password"] = r.FormValue("password")
	utils.SetToken(claims, w)
}

func GetNoteHandler(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims) {
	note := claims["note"].(string)
	password := claims["password"]
	userInputedPassword := r.FormValue("password")
	if password == userInputedPassword {
		w.Write([]byte(note))
		return
	}
	http.Error(w, "Wrong Password!", 401)
}
