'use client';
import { Button, Card, CardBody, CardHeader } from "@nextui-org/react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <Card className="max-w-md">
        <CardHeader className="flex gap-3">
          <div className="flex flex-col">
            <p className="text-xl font-bold">EIS-GPT</p>
          </div>
        </CardHeader>
        <CardBody className="gap-4">
          <p>EIS-GPT: A Q/A platform for documentation</p>
          <p className="text-gray-500">Ready to build...</p>
          <Button color="primary" size="lg" fullWidth>
            Get Started
          </Button>
        </CardBody>
      </Card>
    </main>
  );
}