// k6 Smoke Test - Quick validation that system works
// Run: k6 run perf/smoke.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,           // 1 virtual user
  duration: '30s',  // 30 seconds
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // <1% errors
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5000';

export default function() {
  // Health check
  let res = http.get(`${BASE_URL}/health`);
  check(res, {
    'health check status 200': (r) => r.status === 200,
    'health check has ok': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.ok === true;
      } catch (e) {
        return false;
      }
    },
  });

  sleep(1);

  // Status check
  res = http.get(`${BASE_URL}/status`);
  check(res, {
    'status check 200': (r) => r.status === 200,
    'status operational': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.status === 'operational';
      } catch (e) {
        return false;
      }
    },
  });

  sleep(1);

  // Templates list (optional check - may require auth)
  res = http.get(`${BASE_URL}/api/v1/templates`);
  check(res, {
    'templates list accessible': (r) => r.status === 200 || r.status === 401,
    'has templates': (r) => {
      if (r.status !== 200) return true; // Skip if auth required
      try {
        const body = JSON.parse(r.body);
        return body.templates && body.templates.length > 0;
      } catch (e) {
        return false;
      }
    },
  });

  sleep(1);

  // Metrics summary (optional check - may require auth)
  res = http.get(`${BASE_URL}/api/v1/metrics/summary`);
  check(res, {
    'metrics accessible': (r) => r.status === 200 || r.status === 401,
  });

  sleep(2);
}

export function handleSummary(data) {
  return {
    'perf/results/smoke_summary.json': JSON.stringify(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

function textSummary(data, options) {
  const { indent = '', enableColors = false } = options;
  
  let summary = `\n${indent}Smoke Test Results:\n`;
  summary += `${indent}  Checks passed: ${data.metrics.checks.values.passes}/${data.metrics.checks.values.passes + data.metrics.checks.values.fails}\n`;
  summary += `${indent}  Avg response time: ${data.metrics.http_req_duration.values.avg.toFixed(2)}ms\n`;
  summary += `${indent}  P95 response time: ${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms\n`;
  summary += `${indent}  Failed requests: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%\n`;
  
  return summary;
}
