<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const sds = ref(null)

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:8000/sds/${route.params.id}`)
  sds.value = res.data
})
async function remove() {
  if (!confirm("Are you sure you want to delete this SDS?")) return;

  await axios.delete(`http://127.0.0.1:8000/sds/${route.params.id}`);
  alert("Deleted");
  window.location.href = "/sds";
}

</script>

<template>
  <div v-if="sds" class="wrapper">
    <h1>🧾 {{ sds.filename }}</h1>
    <p><b>Supplier:</b> {{ sds.supplier || "Unknown" }}</p>

    <section>
      <h2>Extracted Data</h2>
      <div class="row"><b>Product Name:</b> {{ sds.extracted.product_name }}</div>
      <div class="row"><b>Signal Word:</b> {{ sds.extracted.signal_word }}</div>
      
      <h3>CAS Numbers</h3>
      <ul><li v-for="c in sds.extracted.cas_numbers">{{ c }}</li></ul>

      <h3>Hazard Statements</h3>
      <ul><li v-for="h in sds.extracted.hazard_statements">{{ h }}</li></ul>

      <h3>Precautionary Statements</h3>
      <ul><li v-for="p in sds.extracted.precautionary_statements">{{ p }}</li></ul>
    </section>

    <button @click="$router.push('/sds')" class="back">⬅ Back</button>
    <button class="del" @click="remove">🗑 Delete SDS</button>

  </div>
</template>

<style scoped>
.wrapper { max-width:800px; margin:auto; padding:30px; color:white; }
section { background:#1b1b1b; padding:20px; border-radius:10px; margin-top:20px; }
.row { margin:5px 0; }
.back { margin-top:20px; padding:10px 20px; background:#4ade80; border-radius:6px; font-weight:bold; }
.del {
  margin-top:10px;
  background:#ff4f4f;
  padding:10px 18px;
  border-radius:8px;
  font-weight:bold;
  color:white;
}
.del:hover { opacity:.8; }

</style>
