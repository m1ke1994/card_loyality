import { test, expect } from "@playwright/test";

test("login link -> dashboard -> qr -> staff verify (mock)", async ({ page }) => {
  await page.route("**/api/v1/auth/telegram/consume", (route) =>
    route.fulfill({ status: 200, body: JSON.stringify({ access: "token", refresh: "refresh" }) })
  );
  await page.route("**/api/v1/tokens/issue", (route) =>
    route.fulfill({ status: 200, body: JSON.stringify({ qr_token: "abc", expires_at: new Date().toISOString() }) })
  );
  await page.goto("http://localhost:5173/auth/telegram?token=abc");
  await expect(page).toHaveTitle(/Loyalty/);
  await page.goto("http://localhost:5173/qr");
  await page.waitForTimeout(500);
  await expect(page.locator("canvas")).toBeVisible();
});
