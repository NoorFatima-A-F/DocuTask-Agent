import { useState, type FormEvent } from 'react';
import { errorMessage } from '../api/client';
import { useAuth } from '../auth';
import { Button, Card, ErrorBox } from '../components/ui';

export function LoginPage() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [identifier, setIdentifier] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      if (mode === 'login') await login(identifier, password);
      else await register(email, identifier, password);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  }

  const input = 'w-full rounded border border-slate-700 bg-slate-950 px-3 py-2';
  return (
    <div className="mx-auto mt-24 max-w-sm">
      <Card title={mode === 'login' ? 'Sign in' : 'Create account'}>
        <form className="space-y-3" onSubmit={submit}>
          {mode === 'register' && (
            <label className="block text-sm">
              Email
              <input className={input} type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </label>
          )}
          <label className="block text-sm">
            {mode === 'login' ? 'Username or email' : 'Username'}
            <input className={input} value={identifier} onChange={(e) => setIdentifier(e.target.value)} required />
          </label>
          <label className="block text-sm">
            Password
            <input
              className={input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <ErrorBox message={error} />
          <Button type="submit" disabled={busy} className="w-full">
            {mode === 'login' ? 'Sign in' : 'Create account'}
          </Button>
        </form>
        <button
          className="mt-3 text-sm text-blue-400 hover:underline"
          onClick={() => {
            setMode(mode === 'login' ? 'register' : 'login');
            setError(null);
          }}
        >
          {mode === 'login' ? 'Need an account? Register' : 'Have an account? Sign in'}
        </button>
      </Card>
    </div>
  );
}
