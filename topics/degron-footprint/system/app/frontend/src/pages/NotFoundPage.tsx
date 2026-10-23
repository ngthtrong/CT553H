import { Link } from 'react-router-dom';
import { useDocumentTitle } from '../lib/hooks';

export function NotFoundPage() {
  useDocumentTitle('Page not found');
  return (
    <>
      <h1>Page not found</h1>
      <p><Link to="/">Go to the input page</Link></p>
    </>
  );
}
