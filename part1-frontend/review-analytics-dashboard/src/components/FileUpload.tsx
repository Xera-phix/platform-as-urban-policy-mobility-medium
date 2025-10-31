import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, File, CheckCircle2, AlertCircle } from 'lucide-react';

interface FileUploadProps {
  onUpload: (file: File) => void;
}

export default function FileUpload({ onUpload }: FileUploadProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    setError(null);
    
    if (rejectedFiles.length > 0) {
      setError('Please upload a valid JSON or CSV file (max 50MB)');
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setUploadedFile(file);
      onUpload(file);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/json': ['.json'],
      'text/csv': ['.csv'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false,
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-3xl mx-auto"
    >
      <div
        {...getRootProps()}
        className={`
          relative border transition-all duration-300 ease-in-out cursor-pointer
          ${isDragActive 
            ? 'border-primary bg-primary/5' 
            : 'border-border hover:border-primary/50 bg-muted/50'
          }
          ${uploadedFile ? 'border-accent bg-accent/5' : ''}
          ${error ? 'border-red-500 bg-red-500/5' : ''}
          h-64 flex items-center justify-center
        `}
      >
        <input {...getInputProps()} />
        
        <AnimatePresence mode="wait">
          {uploadedFile ? (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex flex-col items-center gap-3"
            >
              <CheckCircle2 size={48} className="text-accent" strokeWidth={1.5} />
              <div className="text-center">
                <p className="text-lg font-medium text-foreground">
                  File uploaded
                </p>
                <p className="text-sm text-foreground/50 mt-1 font-light">
                  {uploadedFile.name} • {(uploadedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </motion.div>
          ) : error ? (
            <motion.div
              key="error"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex flex-col items-center gap-3"
            >
              <AlertCircle size={48} className="text-red-500" strokeWidth={1.5} />
              <div className="text-center">
                <p className="text-lg font-medium text-red-500">
                  Upload failed
                </p>
                <p className="text-sm text-foreground/50 mt-1">
                  {error}
                </p>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="upload"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex flex-col items-center gap-4"
            >
              <motion.div
                animate={{ y: isDragActive ? -8 : 0 }}
                transition={{ duration: 0.2 }}
              >
                {isDragActive ? (
                  <File size={48} className="text-primary" strokeWidth={1.5} />
                ) : (
                  <Upload size={48} className="text-foreground/30" strokeWidth={1.5} />
                )}
              </motion.div>
              <div className="text-center">
                <p className="text-base font-medium text-foreground">
                  {isDragActive ? 'Drop file here' : 'Drag & drop your data'}
                </p>
                <p className="text-sm text-foreground/40 mt-2 font-light">
                  JSON or CSV • Maximum 50MB
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
