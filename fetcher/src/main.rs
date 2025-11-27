use anyhow::Result;
use clap::Parser;
use reqwest::blocking::Client;
use serde_json::Value;
use std::fs::File;
use std::io::Write;

#[derive(Parser, Debug)]
struct Args {
    /// Engine API base URL (e.g. http://localhost:8551)
    #[clap(long, default_value = "http://localhost:8551")]
    url: String,

    /// Output filename for the payload JSON
    #[clap(long, default_value = "payload.json")]
    outfile: String,

    /// Fetch block by number: either "latest" or a decimal number
    #[clap(long, default_value = "latest")]
    block: String,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let client = Client::builder().build()?;

    let rpc = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "engine_getPayloadV3",
        "params": [null]
    });

    let resp = client.post(&args.url)
        .json(&rpc)
        .send()?;

    let status = resp.status();
    let v: Value = resp.json()?;

    if !status.is_success() {
        eprintln!("Engine API request failed: {}", status);
        eprintln!("Response: {}", v);
        std::process::exit(1);
    }

    let mut f = File::create(&args.outfile)?;
    let pretty = serde_json::to_string_pretty(&v)?;
    f.write_all(pretty.as_bytes())?;
    println!("Saved payload response to {}", &args.outfile);

    Ok(())
}
