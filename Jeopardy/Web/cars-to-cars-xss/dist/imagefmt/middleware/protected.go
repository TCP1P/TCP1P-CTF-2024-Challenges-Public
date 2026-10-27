package middleware

import (
	"net/http"

	"imagefmt/utils" // replace with the correct import path

	"github.com/dgrijalva/jwt-go"
)

// ProtectedHandler is a middleware that checks for valid JWT claims before invoking the callback
func ProtectedHandler(callback func(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		claims, err := utils.GetClaims(w, r)
		if err != nil {
			http.Error(w, "Invalid token", http.StatusUnauthorized)
			return
		}

		callback(w, r, claims)
	}
}

// PrivilegeHandler is similar to ProtectedHandler but doesn't return an error
func PrivilegeHandler(callback func(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims), allowedRoles []string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		claims, err := utils.GetClaims(w, r)
		if err != nil {
			http.Error(w, "Invalid token", http.StatusUnauthorized)
			return
		}

		role, ok := claims["role"].(string)
		if !ok {
			http.Error(w, "Invalid role format", http.StatusUnauthorized)
			return
		}

		// Check if the role is in the allowedRoles
		if !containsRole(role, allowedRoles) {
			http.Error(w, "Insufficient privileges", http.StatusForbidden)
			return
		}

		callback(w, r, claims)
	}
}

// containsRole checks if a given role is in the allowedRoles
func containsRole(role string, allowedRoles []string) bool {
	for _, allowedRole := range allowedRoles {
		if role == allowedRole {
			return true
		}
	}
	return false
}
