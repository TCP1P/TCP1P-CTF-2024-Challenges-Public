use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::{Aes256Gcm, Nonce};
use image::GenericImageView;
use rand::rngs::OsRng;
use rand::RngCore;
use std::env;
use std::fs::File;
use std::io::{self, BufWriter, Write};
use zstd::stream::Encoder;

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <input.png> <output.skibidi>", args[0]);
        std::process::exit(1);
    }

    let input_path = &args[1];
    let output_path = &args[2];

    let img = image::io::Reader::open(input_path)
        .expect("Failed to open input image")
        .decode()
        .expect("Failed to decode input image");

    let (width, height) = img.dimensions();
    let pixels = img.to_rgba8(); 
    let channels = 4u8; 
    
    let mut compressor = Encoder::new(Vec::new(), 0).expect("Failed to create Zstd encoder");
    compressor
        .write_all(&pixels)
        .expect("Failed to write data to compressor");
    let compressed_data = compressor
        .finish()
        .expect("Failed to compress pixel data");

    let mut key = [0u8; 32];
    let mut iv = [0u8; 12];
    OsRng.fill_bytes(&mut key);
    OsRng.fill_bytes(&mut iv);

    let cipher = Aes256Gcm::new_from_slice(&key).expect("Invalid key length");

    let nonce = Nonce::from_slice(&iv); 
    let ciphertext = cipher
        .encrypt(nonce, compressed_data.as_ref())
        .expect("Encryption failed");

    let output_file = File::create(output_path)?;
    let mut writer = BufWriter::new(output_file);

    writer.write_all(b"SKB1")?; // Magic number
    writer.write_all(&width.to_le_bytes())?; // Width in little endian
    writer.write_all(&height.to_le_bytes())?; // Height in little endian
    writer.write_all(&[channels])?; // Number of channels
    writer.write_all(&[1u8])?; // Compression method identifier (1 for zstd)
    writer.write_all(&key)?; // AES Key (32 bytes)
    writer.write_all(&iv)?; // AES IV (12 bytes)
    writer.write_all(&ciphertext)?;

    println!(
        "Successfully converted '{}' to '{}' with dimensions {}x{}, {} channels, compressed with Zstandard, and encrypted with AES-GCM.",
        input_path, output_path, width, height, channels
    );

    Ok(())
}
