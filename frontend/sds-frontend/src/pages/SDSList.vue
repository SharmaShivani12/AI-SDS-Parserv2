<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const list = ref([])

onMounted(async () => {
  const res = await axios.get("http://127.0.0.1:8000/sds")
  list.value = res.data
})

async function remove(id) {
  if (!confirm("Delete this SDS permanently?")) return;

  await axios.delete(`http://127.0.0.1:8000/sds/${id}`);
  list.value = list.value.filter(i => i.id !== id);
}
</script>

<template>
  <div class="page">
    <h2>📁 Stored SDS Documents</h2>

    <div v-if="list.length===0" class="empty">No SDS uploaded yet.</div>

    <div class="grid">
      <div v-for="item in list" :key="item.id" class="card">
        <h3>📄 {{ item.filename }}</h3>
        <p><b>Supplier:</b> {{ item.supplier || "Unknown" }}</p>
        <p><b>ID:</b> {{ item.id }}</p>
        <router-link :to="'/sds/'+item.id" class="btn">🔍 View Details</router-link>
        <button class="btn delete" @click="remove(item.id)">🗑 Delete</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { padding:30px; text-align:center; color:white; }
.grid {
  display:grid;
  grid-template-columns:repeat(auto-fill, minmax(250px,1fr));
  gap:18px;
  margin-top:25px;
}
.card {
  background:#1b1d22;
  padding:18px;
  border-radius:10px;
  border:1px solid #333;
  transition:.3s;
}
.card:hover { transform:translateY(-4px); border-color:#4ade80; }
.btn {
  margin-top:10px; display:inline-block; background:#4ade80;
  padding:6px 14px; border-radius:6px; font-weight:bold; text-decoration:none; color:#000;
}
.empty { margin-top:35px; font-size:18px; opacity:0.6; }
.btn.view { background:#4ade80; color:#000; }
.btn.delete { background:#ff5252; margin-left:10px; color:white; }
.card button { padding:6px 12px; border-radius:6px; font-weight:bold; cursor:pointer; }
.card button:hover { opacity:.85; }

</style><style scoped>
.page { padding:30px; text-align:center; color:white; }
.page h2 { font-size:26px; color:var(--yellow); }

.grid {
  display:grid;
  grid-template-columns:repeat(auto-fill, minmax(260px,1fr));
  gap:22px;
  padding:20px 40px;
}

.card {
  background:#0f0f0f;
  padding:20px;
  border:1px solid #1f1f1f;
  border-radius:12px;
  transition:.3s;
  color:white;
}
.card:hover { border-color:var(--green); transform:translateY(-4px); }

.btn {
  margin-top:12px;
  background:var(--green);
  color:#000;
  font-weight:bold;
  padding:8px 14px;
  border-radius:6px;
  display:inline-block;
}

.delete {
  background:#ff4f4f;
  color:white;
  margin-left:10px;
}
.delete:hover { background:#ff6b6b; }
</style>

