package handlers

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"imagefmt/utils"
	"net/http"
	"os"
	"time"

	"github.com/dgrijalva/jwt-go"
)

func XorImageHandler(w http.ResponseWriter, r *http.Request, claims jwt.MapClaims) {
	// Retrieve user input
	xorString := r.FormValue("xorString")
	image, err := base64.StdEncoding.DecodeString(r.FormValue("image"))
	if err != nil {
		http.Error(w, "Error retrieving image from form", http.StatusBadRequest)
		return
	}
	if len(image) > (25 << 10) {
		http.Error(w, "Image size is too large", http.StatusBadRequest)
		return
	}

	// Create a unique filename for the uploaded image
	fileName := utils.GenerateRandomFilename(xorString)

	// Save the uploaded image to a file
	filePath := utils.UploadPath + fileName
	if err := utils.SaveFile(bytes.NewReader(image), filePath); err != nil {
		fmt.Println(err)
		http.Error(w, "Error saving image", http.StatusInternalServerError)
		return
	}

	// XOR the image
	outPath := utils.UploadPath + "xor_" + fileName
	err = utils.XorImageByFilename(filePath, outPath, xorString)
	if err != nil {
		os.Remove(filePath)
		fmt.Println(err)
		http.Error(w, "Error XORing image", http.StatusInternalServerError)
		return
	}

	// Serve the XORed image
	w.Header().Set("Content-Type", "image/png")
	xorImageFile, err := os.Open(outPath)
	if err != nil {
		http.Error(w, "Error opening XORed image", http.StatusInternalServerError)
		return
	}
	defer xorImageFile.Close()

	os.Remove(outPath)
	os.Remove(filePath)

	http.ServeContent(w, r, "xor_image.jpg", time.Now(), xorImageFile)
}
