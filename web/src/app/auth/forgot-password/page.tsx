"use client";
import React, { useState } from "react";
import { forgotPassword } from "./utils";
import AuthFlowContainer from "@/components/auth/AuthFlowContainer";
import CardSection from "@/components/admin/CardSection";
import Title from "@/components/ui/title";
import Text from "@/components/ui/text";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await forgotPassword(email);
      setMessage("Password reset email sent. Please check your inbox.");
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  return (
    <AuthFlowContainer>
      <div className="flex flex-col w-full justify-center">
        <CardSection className="mt-4 w-full">
          <div className="flex">
            <Title className="mb-2 mx-auto font-bold">Forgot Password</Title>
          </div>
          <form
            className="w-full flex flex-col items-stretch mt-8"
            onSubmit={handleSubmit}
          >
            <Input
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <Button type="submit" className="w-full">
              Reset Password
            </Button>
          </form>
          {message && (
            <Text className="mt-4 text-center text-sm text-gray-600">
              {message}
            </Text>
          )}
          <div className="flex">
            <Text className="mt-4 mx-auto">
              <Link href="/auth/login" className="text-link font-medium">
                Back to Login
              </Link>
            </Text>
          </div>
        </CardSection>
      </div>
    </AuthFlowContainer>
  );
};

export default ForgotPasswordPage;
