import { useCallback, useRef, useState } from "react";
import type { DragEvent } from "react";

interface UploadDropzoneProps {
  file: File | null;
  onFileSelected: (file: File | null) => void;
}

const ACCEPTED = [".pdf", ".docx", ".txt"];

export default function UploadDropzone({ file, onFileSelected }: UploadDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback(
    (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const dropped = e.dataTransfer.files?.[0];
      if (dropped) onFileSelected(dropped);
    },
    [onFileSelected]
  );

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
        className={`cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-300 ${
          isDragging
            ? "scale-[1.01] border-highlighter-deep bg-highlighter-soft/40 shadow-card-hover"
            : "border-paper-line bg-paper-card hover:-translate-y-0.5 hover:border-ink-faint hover:shadow-card"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED.join(",")}
          className="hidden"
          onChange={(e) => onFileSelected(e.target.files?.[0] ?? null)}
        />
        {file ? (
          <div>
            <p className="font-medium text-ink">{file.name}</p>
            <p className="mt-1 text-sm text-ink-soft">
              {(file.size / 1024).toFixed(0)} KB &middot; click or drop to replace
            </p>
          </div>
        ) : (
          <div>
            <p className="font-medium text-ink">Drop your resume here, or click to browse</p>
            <p className="mt-1 text-sm text-ink-soft">PDF, DOCX, or TXT &middot; up to 8 MB</p>
          </div>
        )}
      </div>
    </div>
  );
}
