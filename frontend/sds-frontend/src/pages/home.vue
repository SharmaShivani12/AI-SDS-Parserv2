<script setup>
import { ref } from "vue";
import axios from "axios";

const file = ref(null);
const loading = ref(false);
const message = ref("");

function onFileChange(e) {
  file.value = e.target.files[0];
  message.value = "";
}

async function upload(normal = true) {
  if (!file.value) return (message.value = "⚠ Please select a file first");
  loading.value = true;

  const form = new FormData();
  if (normal) form.append("files", file.value);
  else form.append("file", file.value);

  const url = normal
    ? "http://127.0.0.1:8000/upload"
    : "http://127.0.0.1:8000/extract-ai";

  try {
    await axios.post(url, form);
    message.value = normal
      ? "📄 Uploaded successfully"
      : "🤖 AI Extraction complete & saved!";
  } catch (err) {
    message.value = "❌ Upload failed";
    console.log(err);
  }

  loading.value = false;
}
</script>

<template>
  <div class="wrapper">
    <div class="card">
      <h1>🧪 AI SDS Parser</h1>
      <p class="subtitle">Upload Safety Data Sheet PDF & extract chemicals automatically</p>

      <input type="file" @change="onFileChange" class="file-input" />

      <div class="btn-group">
        <button class="btn" @click="upload(true)">Upload (Normal)</button>
        <button class="btn green" @click="upload(false)">Upload using AI (Phi-3/LLaMA)</button>
      </div>

      <p v-if="loading" class="loading">⏳ Extracting...</p>
      <p v-if="message" class="msg">{{ message }}</p>

      <router-link to="/sds" class="view-link">📁 View Stored SDS →</router-link>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  display:flex;
  justify-content:center;
  padding-top:45px;
  min-height:100vh;
  background:black;
}

.card {
  background:DimGrey;
  width:520px;
  height:480px;
  padding:40px;
  border-radius:16px;
  border:1px solid #A9A9A9;
  box-shadow:0 0 30px rgba(0,0,0,.8);
  text-align:center;
}

h1 { font-size:32px; margin-bottom:10px; color:#FAEBD7; }
.subtitle { color:#FAEBD7; font-size:14px;font-weight:700; margin-bottom:25px; }

.file-input {
  width: 100%;
  padding: 12px;
  background: DarkSeaGreen;   /* Soft aqua shade */
  color: black;
  border: 1px solid ;
  border-radius: 8px;
  
  border:1px solid DarkSeaGreen;
  margin-bottom: 15px;   /* 🔥 Now applied correctly */
}


.btn-group {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* Main Button */
.btn {
  background: #fa972ed3;
  padding: 12px 20px;
  border-radius: 8px;
  border:1px solid  #804b12d3;
  font-weight: 700;         
  font-size: 1rem;           
  color: #010000ff;
  cursor: pointer;
  transition: 0.25s;
}
.btn:hover {
  background: #708090;
}

/* AI Button Variant */
.green {
  background: Khaki;
  color: #000;
  font-weight: 800; 
  border:1px solid  Khaki         /* 🔥 Even bolder for attention */
}
.green:hover {
  background: #708090;
  color: white;
}

.msg { color:#ffe95e; margin-top:10px; }
.loading { color:#00ff9d; margin-top:10px; }

.view-link {
  display:block;
  margin-top:25px;
  font-size:18px;
  color:#FAEBD7;
  font-weight:bold;
}
.view-link:hover { color:#fff78a; }
</style>
