// LogoutHandler handles user logout by clearing the JWT token cookie
package handlers

import (
	"imagefmt/utils"
	"net/http"

	"github.com/dgrijalva/jwt-go"
)

func LogoutHandler(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims) {
	// Clear the token cookie
	utils.SetCookie("", w)

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Logout successful"))
}
