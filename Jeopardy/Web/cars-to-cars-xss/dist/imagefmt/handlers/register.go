package handlers

import (
	"database/sql"
	"imagefmt/utils"
	"net/http"
)

func RegisterHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		username := r.FormValue("username")
		password := r.FormValue("password")

		if username == "" || password == "" {
			http.Error(w, "Invalid credentials", http.StatusUnauthorized)
			return
		}

		// Insert user into the database
		_, err := db.Exec("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", username, password, "user")

		if err != nil {
			http.Error(w, "User already exist", http.StatusInternalServerError)
			return
		}

		if err := utils.SetToken(map[string]interface{}{
			"id":   username,
			"role": "user",
		}, w); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		w.Write([]byte("User registered successfully"))
	}
}
