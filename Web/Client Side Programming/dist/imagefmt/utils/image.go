package utils

import (
	"fmt"
	"image"
	"image/color"
	_ "image/jpeg"
	"image/png"
	"os"
)

func readImage(filename string) (image.Image, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	img, _, err := image.Decode(file)
	if err != nil {
		return nil, err
	}

	return img, nil
}

func xorImage(img image.Image, xorString string) image.Image {
	bounds := img.Bounds()
	width, height := bounds.Dx(), bounds.Dy()

	newImg := image.NewNRGBA(bounds)

	xorLen := len(xorString)
	xorIndex := 0

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			colorAt := img.At(x, y)

			r, g, b, a := colorAt.RGBA()

			xorChar := xorString[xorIndex]

			xorR := uint8(r>>8) ^ xorChar
			xorG := uint8(g>>8) ^ xorChar
			xorB := uint8(b>>8) ^ xorChar

			newColor := color.NRGBA{xorR, xorG, xorB, uint8(a >> 8)}

			newImg.SetNRGBA(x, y, newColor)

			xorIndex = (xorIndex + 1) % xorLen
		}
	}

	return newImg
}

func XorImageByFilename(filename string, out string, xorString string) error {
	img, err := readImage(filename)
	if err != nil {
		return fmt.Errorf("error reading image: %s", err)
	}

	newImg := xorImage(img, xorString)

	newFile, err := os.Create(out)
	if err != nil {
		return fmt.Errorf("error creating new image file: %s", err)
	}
	defer newFile.Close()

	err = png.Encode(newFile, newImg)
	if err != nil {
		return fmt.Errorf("error encoding new image: %s", err)
	}
	return nil
}
