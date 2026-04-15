import { Link } from "react-router";
import BrandMark from "../brand/BrandMark";
import LanguageSwitcher from "./LanguageSwitcher";

export default function TopNav({ homeLink = true }) {
  const BrandWrapper = homeLink ? Link : "div";
  const brandProps = homeLink ? { to: "/" } : {};

  return (
    <header className="-mx-5 mb-10 border-b border-white/5 px-5 py-3.5 md:-mx-7 md:px-7 lg:-mx-8 lg:px-8">
      <div className="flex items-center justify-between">
        <BrandWrapper
          {...brandProps}
          className="flex items-center gap-2.5"
        >
          <BrandMark />
          <span className="text-2xl font-semibold tracking-tight text-white">
            GRS
          </span>
        </BrandWrapper>

        <LanguageSwitcher />
      </div>
    </header>
  );
}