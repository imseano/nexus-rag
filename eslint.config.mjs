import tseslint from 'typescript-eslint'
import eslintConfigPrettier from 'eslint-config-prettier'

export default tseslint.config(
  { ignores: ['**/node_modules', '**/dist', '**/out', '.gitignore'] },
  tseslint.configs.recommended,
  {
    settings: {
      react: {
        version: 'detect'
      }
    }
  },
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
    },
    rules: {
      'no-unused-vars': 'off',
      'explicit-function-return-type': 'off'
    }
  },
  eslintConfigPrettier
)
