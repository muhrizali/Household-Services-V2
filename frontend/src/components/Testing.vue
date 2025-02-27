<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { Field, Form } from 'vee-validate';

let data = ref("NO DATA");
let loading = ref(false);

function getAPI(url) {
    const config = {
        baseURL: "http://127.0.0.1:5000",
        headers: { "Content-Type": "application/json" }
    };
    return axios.get(url, config);
}

function onClickRequest() {
    loading.value = true;
    getAPI("/customer")
        .then((response) => data.value = response.data)
        .catch((error) => data.value = error)
        .finally(() => loading.value = false)
}

function onSubmit(values) {
    console.log(values);
}

</script>
<template>
    <!-- NEW -->
    <Form @submit="onSubmit" class="card-body form-control">
      <h2 class="card-title text-2xl text-center">Customer Signup</h2>
      <Field name="email" type="email" class="input input-bordered" placeholder="Email"/>

      <button class="btn btn-primary">Sign Up</button>
    </Form>


</template>