package utils

import (
	"fmt"
	"net/http"

	"github.com/dgrijalva/jwt-go"
)

type JWTAuthenticator struct {
	secret string
}

func NewJWT(secret string) JWTAuthenticator {
	return JWTAuthenticator{secret: secret}
}

func (g *JWTAuthenticator) GenerateToken(claims map[string]interface{}) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims(claims))

	tokenString, err := token.SignedString([]byte(g.secret))
	if err != nil {
		return "", err
	}

	return tokenString, nil
}

func (auth *JWTAuthenticator) ParseToken(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(auth.secret), nil
	})
	if err != nil {
		return nil, err
	}
	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims, nil
	}
	return nil, fmt.Errorf("invalid token")
}

// GetClaims extracts and validates JWT claims from the request
func GetClaims(w http.ResponseWriter, r *http.Request) (jwt.MapClaims, error) {
	// Get the JWT token from the cookie
	cookie, err := r.Cookie(CookieName)
	if err != nil {
		return nil, fmt.Errorf("Unauthorized")
	}

	// Parse the JWT token
	auth := NewJWT(SecretKey)
	claims, err := auth.ParseToken(cookie.Value)
	if err != nil {
		http.Error(w, "Invalid token", http.StatusUnauthorized)
		return nil, fmt.Errorf("Unauthorized")
	}
	return claims, nil
}
