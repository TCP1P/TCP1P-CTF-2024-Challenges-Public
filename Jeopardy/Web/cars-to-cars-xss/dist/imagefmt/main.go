package main

import (
	"database/sql"
	"fmt"
	"imagefmt/handlers"
	"imagefmt/middleware"
	"net/http"

	"github.com/google/uuid"
	"github.com/gorilla/csrf"
	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

const (
	dbPath = "./users.db"
	port   = 8080
)

func main() {
	// Create SQLite database
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		fmt.Println("Error opening database:", err)
		return
	}
	defer db.Close()

	// Create users table if not exists
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL,
		role TEXT NOT NULL
	)`)
	if err != nil {
		fmt.Println("Error creating users table:", err)
		return
	}
	CSRF := csrf.Protect([]byte(uuid.New().String()))
	router := mux.NewRouter()

	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(csrf.Token(r)))
	})
	router.HandleFunc("/register", handlers.RegisterHandler(db))
	router.HandleFunc("/login", handlers.LoginHandler(db))
	router.HandleFunc("/logout", middleware.ProtectedHandler(handlers.LogoutHandler))
	router.HandleFunc("/image/xor", middleware.ProtectedHandler(handlers.XorImageHandler))
	router.HandleFunc("/image/setnote", middleware.ProtectedHandler(handlers.SetNoteHandler))
	router.HandleFunc("/image/getnote", middleware.ProtectedHandler(handlers.GetNoteHandler))
	router.HandleFunc("/note/get", middleware.ProtectedHandler(handlers.GetNoteHandler))
	router.HandleFunc("/note/set", middleware.ProtectedHandler(handlers.SetNoteHandler))
	router.NotFoundHandler = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Missing " + r.URL.Path + " path"))
	})
	fmt.Printf("Server is running on http://localhost:%d\n", port)
	http.ListenAndServe(fmt.Sprintf(":%d", port), CSRF(router))
}
