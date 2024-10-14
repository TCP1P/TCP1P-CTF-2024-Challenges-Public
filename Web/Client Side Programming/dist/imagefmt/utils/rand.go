package utils

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"path/filepath"
)

func GenerateRandomFilename(inputFilename string) string {
	ext := filepath.Ext(inputFilename)

	hasher := md5.New()
	hasher.Write([]byte(inputFilename))
	hash := hex.EncodeToString(hasher.Sum(nil))

	randomFilename := fmt.Sprintf("%s%s", hash, ext)

	return randomFilename
}
