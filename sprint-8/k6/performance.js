
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '20s', target: 10 },
    { duration: '5s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5000';

export default function () {
  const itemsRes = http.get(`${BASE_URL}/api/items`);

  check(itemsRes, {
    'items status is 200': (r) => r.status === 200,
  });

  const dataRes = http.get(`${BASE_URL}/api/data`);

  check(dataRes, {
    'data status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
