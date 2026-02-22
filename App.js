import React, { useState } from 'react';

export default function GardenApp() {
  const [image, setImage] = useState(null);
  const [beds, setBeds] = useState([]);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    // Preview the image on your phone
    setImage(URL.createObjectURL(file));
    
    // This sends the photo to your Python "Brain" (server.py)
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await fetch('http://localhost:8000/scan-garden', { 
        method: 'POST', 
        body: formData 
      });
      const data = await res.json();
      setBeds(data.beds);
    } catch (err) {
      console.error("Make sure your backend is running!", err);
    }
  };

  return (
    <div style={{ 
      background: '#1c1917', 
      minHeight: '100vh', 
      padding: '20px', 
      color: 'white', 
      fontFamily: 'sans-serif',
      textAlign: 'center' 
    }}>
      <h1 style={{ color: '#10b981' }}>🌿 Dr. Greenthumb AI</h1>
      <p>Upload a photo of your garden to scan for beds</p>
      
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleUpload} 
        style={{ margin: '20px 0', padding: '10px', background: '#292524', border: 'none', color: 'white' }}
      />

      <div style={{ position: 'relative', marginTop: '20px', maxWidth: '100%', overflow: 'hidden' }}>
        {image && (
          <img 
            src={image} 
            alt="Garden" 
            style={{ width: '100%', borderRadius: '15px', display: 'block' }} 
          />
        )}
        
        {/* This draws the green boxes over the garden beds found by the AI */}
        {beds.map((bed) => (
          <div key={bed.id} style={{
            position: 'absolute', 
            border: '3px solid #10b981', 
            background: 'rgba(16, 185, 129, 0.3)',
            left: bed.x, 
            top: bed.y, 
            width: bed.width, 
            height: bed.height,
            borderRadius: '4px'
          }} />
        ))}
      </div>
    </div>
  );
}
