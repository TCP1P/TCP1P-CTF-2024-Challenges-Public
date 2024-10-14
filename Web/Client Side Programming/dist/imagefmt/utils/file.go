package utils

import (
	"fmt"
	"io"
	"os"
)

func SaveFile(file io.Reader, filePath string) error {
	out, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("error creating file: %s", err)
	}
	defer out.Close()

	_, err = io.Copy(out, file)
	if err != nil {
		return fmt.Errorf("error copying file content: %s", err)
	}

	return nil
}
