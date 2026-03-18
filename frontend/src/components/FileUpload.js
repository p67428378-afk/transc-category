import React from 'react';

const FileUpload = ({ onFileChange, onFileUpload, loading, error }) => {
  return (
    <section className="upload-section">
      <h2>Upload Transactions (CSV)</h2>
      <input type="file" accept=".csv" onChange={onFileChange} />
      <button onClick={onFileUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload & Process'}
      </button>
      {error && <p className="error-message">{error}</p>}
    </section>
  );
};

export default FileUpload;
