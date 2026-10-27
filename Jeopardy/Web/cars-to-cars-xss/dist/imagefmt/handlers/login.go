package handlers

import (
	"database/sql"
	"imagefmt/utils"
	"net/http"
)

// LoginHandler handles user login and issues a JWT token
func LoginHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		username := r.FormValue("username")
		password := r.FormValue("password")
		if username == "" || password == "" {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		var userRole string
		err := db.QueryRow("SELECT role FROM users WHERE username=? AND password=?", username, password).Scan(&userRole)
		if err != nil {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		// Set the token in a cookie
		if err := utils.SetToken(map[string]interface{}{
			"id":   username,
			"role": userRole,
		}, w); err != nil {
			http.Error(w, err.Error(), http.StatusUnauthorized)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Login successful"))
	}
}
