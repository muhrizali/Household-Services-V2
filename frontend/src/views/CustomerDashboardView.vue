<script setup>
import { logoutUser } from '@/fns';
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const customerID = route.params.id;

const customerFound = ref(false);
const customer = ref({});

const message = ref('');


async function initialLoad() {
  const response = await getAPI({ url: '/api/customer', params: { 'id': customerID } });
  if (response.data.found) {
    customerFound.value = true;
    customer.value = response.data.customer;
  } else {
    message.value = 'Customer Not Found';
  }
}

async function onLogoutClick() {
  logoutUser();
  router.push({ name: 'login' });
}

onMounted(initialLoad);

</script>
<template>
    <div class="font-fira">
      <!-- Base structure: After Login -->
      <!-- Header / Logo / Site -->
      <nav class="navbar bg-primary">
        <div class="navbar-start">
          <RouterLink to="/testing" class="btn btn-lg btn-ghost text-2xl">
            Welcome, {{ customerFound ? customer.user.fullname : 'Error' }} <span class="opacity-60">[CUSTOMER]</span>
          </RouterLink>
        </div>

        <div class="navbar-center">
          <ul class="menu menu-lg menu-horizontal">

            <li><RouterLink :to="{ name: 'customer_home', params: { id: customerID } }" class="btn btn-ghost">Home</RouterLink></li>
            <li><RouterLink :to="{ name: 'customer_search' }" class="btn btn-ghost">Search</RouterLink></li>
          </ul>
        </div>
        <div class="navbar-end">
          <RouterLink :to="{ name: 'customer_profile_details', params: { id: customerID } }" class="btn btn-ghost text-lg"> Profile </RouterLink>
          <button @click.prevent="onLogoutClick" class="btn btn-ghost text-lg"> Logout </button>
        </div>
      </nav>

      <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
        <RouterView />
      </div>
    </div>
</template>
