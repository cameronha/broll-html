// Apple Vision subject lift (same feature as long-press in Photos). Free, local.
// usage: swift lift.swift in.jpg mask.png
// Writes a grayscale mask, same size as the input. White = subject.
import AppKit
import CoreImage
import Vision

let args = CommandLine.arguments
guard args.count == 3 else { print("usage: lift in.jpg mask.png"); exit(1) }
let inURL = URL(fileURLWithPath: args[1]), outURL = URL(fileURLWithPath: args[2])

let handler = VNImageRequestHandler(url: inURL)
let req = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let obs = req.results?.first, !obs.allInstances.isEmpty else {
    print("no subject found"); exit(2)
}
let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
let ci = CIImage(cvPixelBuffer: buf)
let ctx = CIContext()
guard let cg = ctx.createCGImage(ci, from: ci.extent) else { exit(3) }
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: outURL)
// one extra mask per instance: mask-1.png, mask-2.png ...
for (k, inst) in obs.allInstances.sorted().enumerated() {
    let b = try obs.generateScaledMaskForImage(forInstances: [inst], from: handler)
    let im = CIImage(cvPixelBuffer: b)
    let c = ctx.createCGImage(im, from: im.extent)!
    let u = outURL.deletingPathExtension().path
    try NSBitmapImageRep(cgImage: c).representation(using: .png, properties: [:])!
        .write(to: URL(fileURLWithPath: "\(u)-\(k + 1).png"))
}
print("instances: \(obs.allInstances.count)  size: \(cg.width)x\(cg.height)")
