use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::{Aes256Gcm, Nonce};
use image::{ImageBuffer, Rgba};
use std::env;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;
use zstd::stream::Decoder;

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <input.skibidi>", args[0]);
        std::process::exit(1);
    }

    let input_path = &args[1];
    let mut file = File::open(input_path)?;

    let mut magic = [0u8; 4];
    file.read_exact(&mut magic)?;
    if &magic != b"SKB1" {
        eprintln!("Invalid file format.");
        std::process::exit(1);
    }

    let mut width_bytes = [0u8; 4];
    file.read_exact(&mut width_bytes)?;
    let width = u32::from_le_bytes(width_bytes);

    let mut height_bytes = [0u8; 4];
    file.read_exact(&mut height_bytes)?;
    let height = u32::from_le_bytes(height_bytes);

    let mut channels = [0u8; 1];
    file.read_exact(&mut channels)?;
    let channels = channels[0];

    let mut compression_method = [0u8; 1];
    file.read_exact(&mut compression_method)?;
    let compression_method = compression_method[0];

    let mut key = [0u8; 32];
    file.read_exact(&mut key)?;

    let mut iv = [0u8; 12];
    file.read_exact(&mut iv)?;

    println!(
        "SKB1 Image - Width: {}, Height: {}, Channels: {}",
        width, height, channels
    );
    println!("Compression Method: {}", match compression_method {
        1 => "Zstandard (zstd)",
        _ => "Unknown",
    });
    println!("AES Key: {:02x?}", key);
    println!("AES IV: {:02x?}", iv);

    let mut ciphertext = Vec::new();
    file.read_to_end(&mut ciphertext)?;

    let cipher = Aes256Gcm::new_from_slice(&key).expect("Invalid key length");

    let nonce = Nonce::from_slice(&iv);
    let decrypted_compressed_data = match cipher.decrypt(nonce, ciphertext.as_ref()) {
        Ok(data) => data,
        Err(_) => {
            eprintln!("Decryption failed. Incorrect key or corrupted data.");
            std::process::exit(1);
        }
    };

    let mut decoder = Decoder::new(&decrypted_compressed_data[..])
        .expect("Failed to create Zstd decoder");
    let mut decompressed_data = Vec::new();
    decoder
        .read_to_end(&mut decompressed_data)
        .expect("Failed to decompress data");

    let expected_len = (width as usize) * (height as usize) * (channels as usize);
    if decompressed_data.len() != expected_len {
        eprintln!(
            "Decompressed data size mismatch. Expected: {}, Found: {}",
            expected_len,
            decompressed_data.len()
        );
        std::process::exit(1);
    }

    if channels != 4 {
        eprintln!(
            "Unsupported number of channels: {}. Only RGBA (4) is supported.",
            channels
        );
        std::process::exit(1);
    }

    let img_buffer: ImageBuffer<Rgba<u8>, Vec<u8>> =
        ImageBuffer::from_raw(width, height, decompressed_data)
            .expect("Failed to create image buffer");

    let output_image_path = Path::new(input_path)
        .with_extension("decrypted.png");
    img_buffer
        .save(&output_image_path)
        .expect("Failed to save decrypted image");

    println!(
        "Decrypted and decompressed image saved as '{}'.",
        output_image_path.display()
    );

    Ok(())
}
